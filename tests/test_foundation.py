import copy, json, unittest
from pathlib import Path
from coopai.policy import quota_bytes, gb
from coopai.planner import plan
from benchmarks.ollama_local import consume_stream

ROOT=Path(__file__).resolve().parents[1]

class QuotaTests(unittest.TestCase):
    def test_normal_and_pressure(self):
        self.assertEqual(quota_bytes(gb(36),gb(12),gb(2)),7_200_000_000)
        self.assertEqual(quota_bytes(gb(16),gb(1),gb(2)),0)
    def test_personal_limit(self):
        self.assertEqual(quota_bytes(gb(36),gb(12),gb(2),20,gb(1)),gb(1))
    def test_bad_numbers_are_rejected(self):
        for value in (-1,"NaN","Infinity",True):
            with self.subTest(value=value),self.assertRaises(ValueError): gb(value)
        with self.assertRaises(ValueError): quota_bytes(10,11,0)
        with self.assertRaises(ValueError): quota_bytes(10,8,0,101)

class PlacementTests(unittest.TestCase):
    def setUp(self): self.cfg=json.loads((ROOT/"examples/mac_circle.json").read_text())
    def test_all_layers_once_with_complete_budget(self):
        result=plan(self.cfg);self.assertTrue(result['feasible'])
        assigned=[]
        for s in result['stages']:
            assigned.extend(range(s['layer_start'],s['layer_end_exclusive']))
            self.assertLessEqual(s['reserved_bytes'],s['quota_bytes'])
            self.assertGreater(s['reserved_bytes'],gb(.6))
        self.assertEqual(assigned,list(range(32)))
    def test_no_partial_admission(self):
        cfg=copy.deepcopy(self.cfg)
        for node in cfg['nodes']: node['available_gb']=1
        result=plan(cfg);self.assertFalse(result['feasible']);self.assertEqual(result['stages'],[])
    def test_trust_and_backend_are_hard_filters(self):
        cfg=copy.deepcopy(self.cfg)
        for node in cfg['nodes']: node['trust_group']='other'
        result=plan(cfg);self.assertFalse(result['feasible'])
        cfg=copy.deepcopy(self.cfg)
        for node in cfg['nodes']: node['backend']='other-engine'
        self.assertFalse(plan(cfg)['feasible'])
    def test_duplicate_identity_rejected(self):
        self.cfg['nodes'].append(self.cfg['nodes'][0])
        with self.assertRaises(ValueError): plan(self.cfg)
    def test_nonuniform_model_rejected(self):
        self.cfg['model']['uniform_layer_estimate']=False
        with self.assertRaises(ValueError): plan(self.cfg)

class BenchmarkTests(unittest.TestCase):
    def test_stream_separates_thinking_from_visible_text(self):
        stream=[json.dumps(x).encode() for x in [
            {'thinking':'internal','done':False}, {'response':'bonjour','done':False},
            {'done':True,'eval_count':4,'eval_duration':2_000_000_000}]]
        times=iter([.2,.3,.4,.9])
        r=consume_stream(stream,clock=lambda: next(times),start=0)
        self.assertEqual(r['first_activity_seconds'],.2)
        self.assertEqual(r['first_visible_text_seconds'],.3)
        self.assertEqual(r['server_decode_tokens_per_s'],2)
        self.assertNotIn('response',r)
    def test_truncation_is_failure(self):
        with self.assertRaises(RuntimeError): consume_stream([b'{"response":"partial"}'])
    def test_error_is_failure(self):
        with self.assertRaises(RuntimeError): consume_stream([b'{"error":"no memory"}'])
    def test_empty_completion_and_zero_duration(self):
        r=consume_stream([b'{"done":true,"eval_count":0,"eval_duration":0}'])
        self.assertIsNone(r['first_visible_text_seconds']);self.assertIsNone(r['server_decode_tokens_per_s'])

if __name__=='__main__': unittest.main()
