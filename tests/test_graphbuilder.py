from unittest import TestCase
from openeo.graphbuilder import GraphBuilder


class GraphBuilderTest(TestCase):

    def test_create_empty(self):
        builder = GraphBuilder()
        builder.process("sum",{})
        self.assertEqual(1,len(builder.processes))


    def test_create_from_existing(self):
        graph = {
            "sum_01": {
                "arguments": {
                    "data1": {
                        "from_node": "node1"
                    },
                    "data2": {
                        "from_node": "node3"
                    }
                },
                "process_id":"sum",
                "result": True
            },
            "sum_02": {
                "arguments": {
                    "data": {
                        "from_node": "node4"
                    }
                },
                "process_id": "sum",
            }
        }

        builder = GraphBuilder(graph)

        print(builder.processes)
        self.assertEqual(2,builder.id_counter["sum"])

    def test_merge(self):
        graph1 = {
            "sum1": {
                "arguments": {
                    "data1": {
                        "from_node": "node1"
                    },
                    "data2": {
                        "from_node": "node3"
                    }
                },
                "process_id": "sum",
                "result": True
            }

        }

        graph2 = {
            "sum1": {
                "arguments": {
                    "data": {
                        "from_node": "node4"
                    },
                    "data2": [
                        {
                            "from_node": "node4"
                        }
                    ]
                },
                "process_id": "sum",
            },
            "sum2": {
                "arguments": {
                    "data": {
                        "from_node": "sum1"
                    },
                    "data2": [
                        {
                            "from_node": "sum1"
                        }
                    ]
                },
                "process_id": "sum",
            }
        }

        builder1 = GraphBuilder(graph1)
        builder2 = GraphBuilder(graph2)

        merged = builder1.merge(builder2).processes

        import json
        print(json.dumps(merged, indent=2))
        self.assertIn("sum1", merged)
        self.assertIn("sum2",merged)
        self.assertIn("sum3", merged)
        self.assertEqual("sum2",merged["sum3"]["arguments"]["data"]["from_node"])
        self.assertEqual("sum2", merged["sum3"]["arguments"]["data2"][0]["from_node"])
