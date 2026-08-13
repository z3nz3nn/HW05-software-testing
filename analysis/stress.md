# JTL analysis: 23127373_Stress_20260814.jtl

Generated from the raw CSV JTL using the **nearest-rank** percentile method.
Transaction Controller rows are excluded from endpoint totals to avoid double counting.

## Overall endpoint metrics

| Samples | Error % | Mean ms | p50 ms | p90 ms | p95 ms | p99 ms | Max ms | Samples/s |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 139140 | 0.0 | 42.434 | 39.0 | 85.0 | 95.0 | 112.0 | 256.0 | 290.4826 |

## Per-label metrics

| Label | Samples | Error % | Mean ms | p95 ms | p99 ms | Max ms | Samples/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `01_POST_register` | 46390 | 0.0 | 43.754 | 97.0 | 116.0 | 256.0 | 96.8484 |
| `02_GET_admin_users` | 46380 | 0.0 | 40.48 | 92.0 | 110.0 | 253.0 | 96.9269 |
| `03_DELETE_registered_user` | 46370 | 0.0 | 43.067 | 94.0 | 110.0 | 250.0 | 96.9266 |

## Response codes

```json
{
  "200": 139140
}
```
