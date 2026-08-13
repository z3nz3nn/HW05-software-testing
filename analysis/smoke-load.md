# JTL analysis: 23127373_Load_20260814.jtl

Generated from the raw CSV JTL using the **nearest-rank** percentile method.
Transaction Controller rows are excluded from endpoint totals to avoid double counting.

## Overall endpoint metrics

| Samples | Error % | Mean ms | p50 ms | p90 ms | p95 ms | p99 ms | Max ms | Samples/s |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 546 | 0.0 | 4.918 | 5.0 | 7.0 | 9.0 | 12.0 | 67.0 | 80.3414 |

## Per-label metrics

| Label | Samples | Error % | Mean ms | p95 ms | p99 ms | Max ms | Samples/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `01_POST_register` | 182 | 0.0 | 6.731 | 9.0 | 14.0 | 67.0 | 26.8199 |
| `02_GET_admin_users` | 182 | 0.0 | 1.709 | 3.0 | 4.0 | 4.0 | 28.9394 |
| `03_DELETE_registered_user` | 182 | 0.0 | 6.313 | 9.0 | 16.0 | 18.0 | 29.4308 |

## Response codes

```json
{
  "200": 546
}
```
