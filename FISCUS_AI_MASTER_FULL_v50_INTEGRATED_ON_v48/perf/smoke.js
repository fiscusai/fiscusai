// k6 example: GET /live and /ready
import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  vus: 5,
  duration: '30s',
};

export default function() {
  const base = __ENV.API_URL || 'http://localhost:8000';
  let res = http.get(`${base}/live`);
  check(res, { 'live ok': (r) => r.status === 200 });
  res = http.get(`${base}/ready`);
  check(res, { 'ready ok': (r) => r.status === 200 });
  sleep(1);
}