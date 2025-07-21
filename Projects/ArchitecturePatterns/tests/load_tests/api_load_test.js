import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Ramp up to 20 users
    { duration: '1m', target: 20 },  // Stay at 20 users
    { duration: '30s', target: 0 },  // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.01'],   // Less than 1% of requests should fail
  },
};

export default function () {
  const BASE_URL = 'http://localhost:8888';

  // Test the health endpoint
  const healthCheck = http.get(`${BASE_URL}/health`);
  check(healthCheck, {
    'health check status is 200': (r) => r.status === 200,
  });

  // Create an item
  const createItem = http.post(`${BASE_URL}/items/`, {
    name: `test_item_${Date.now()}`,
  });
  check(createItem, {
    'create item status is 200': (r) => r.status === 200,
  });

  // List items
  const listItems = http.get(`${BASE_URL}/items/`);
  check(listItems, {
    'list items status is 200': (r) => r.status === 200,
  });

  sleep(1);
} 