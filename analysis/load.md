# JTL analysis: 23127373_Load_20260814.jtl

Generated from the raw CSV JTL using the **nearest-rank** percentile method.
Transaction Controller rows are excluded from endpoint totals to avoid double counting.

## Overall endpoint metrics

| Samples | Error % | Mean ms | p50 ms | p90 ms | p95 ms | p99 ms | Max ms | Samples/s |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 19311 | 0.0 | 5.317 | 4.0 | 6.0 | 8.0 | 15.0 | 777.0 | 64.5805 |

## Per-label metrics

| Label | Samples | Error % | Mean ms | p95 ms | p99 ms | Max ms | Samples/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `01_POST_register` | 6437 | 0.0 | 8.186 | 8.0 | 42.0 | 777.0 | 21.5275 |
| `02_GET_admin_users` | 6437 | 0.0 | 2.556 | 5.0 | 12.0 | 639.0 | 21.5592 |
| `03_DELETE_registered_user` | 6437 | 0.0 | 5.209 | 8.0 | 14.0 | 441.0 | 21.5667 |

## Response codes

```json
{
  "200": 19311
}
```
