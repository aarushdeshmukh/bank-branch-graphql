"""
Test Suite for Bank Branches GraphQL API
Tests all GraphQL queries and endpoints.
"""

import unittest
import json
from app import app
from database import init_db

class BankAPITestCase(unittest.TestCase):
    """Test cases for the Bank Branches API"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database once for all tests"""
        init_db()
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_home_endpoint(self):
        """Test home endpoint returns correct response"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'running')
        self.assertIn('graphql', data['endpoints'])
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_graphql_endpoint_exists(self):
        """Test GraphQL endpoint is accessible"""
        query = '{ __schema { queryType { name } } }'
        response = self.client.post('/gql', 
            data=json.dumps({'query': query}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_query_branches(self):
        """Test querying branches with bank details"""
        query = """
        query {
            branches(first: 5) {
                edges {
                    node {
                        ifsc
                        branch
                        city
                        state
                        bank {
                            name
                        }
                    }
                }
            }
        }
        """
        response = self.client.post('/gql',
            data=json.dumps({'query': query}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check response structure
        self.assertIn('data', data)
        self.assertIn('branches', data['data'])
        self.assertIn('edges', data['data']['branches'])
        
        # Check if we got results
        if len(data['data']['branches']['edges']) > 0:
            first_branch = data['data']['branches']['edges'][0]['node']
            self.assertIn('ifsc', first_branch)
            self.assertIn('branch', first_branch)
            self.assertIn('bank', first_branch)
            self.assertIn('name', first_branch['bank'])
    
    def test_query_banks(self):
        """Test querying all banks"""
        query = """
        query {
            banks(first: 5) {
                edges {
                    node {
                        id
                        name
                    }
                }
            }
        }
        """
        response = self.client.post('/gql',
            data=json.dumps({'query': query}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('data', data)
        self.assertIn('banks', data['data'])
    
    def test_query_branch_by_ifsc(self):
        """Test querying a specific branch by IFSC code"""
        # First get an IFSC code
        query_all = """
        query {
            branches(first: 1) {
                edges {
                    node {
                        ifsc
                    }
                }
            }
        }
        """
        response = self.client.post('/gql',
            data=json.dumps({'query': query_all}),
            content_type='application/json')
        
        data = json.loads(response.data)
        
        if len(data['data']['branches']['edges']) > 0:
            ifsc_code = data['data']['branches']['edges'][0]['node']['ifsc']
            
            # Now query for that specific IFSC
            query_specific = f"""
            query {{
                branchByIfsc(ifsc: "{ifsc_code}") {{
                    ifsc
                    branch
                    bank {{
                        name
                    }}
                }}
            }}
            """
            response = self.client.post('/gql',
                data=json.dumps({'query': query_specific}),
                content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('branchByIfsc', data['data'])
            self.assertEqual(data['data']['branchByIfsc']['ifsc'], ifsc_code)
    
    def test_invalid_query(self):
        """Test that invalid queries return errors"""
        query = "{ invalidField }"
        response = self.client.post('/gql',
            data=json.dumps({'query': query}),
            content_type='application/json')
        
        data = json.loads(response.data)
        self.assertIn('errors', data)

if __name__ == '__main__':
    unittest.main()
