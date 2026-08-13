# JTL analysis: 23127373_Soak_20260814.jtl

Generated from the raw CSV JTL using the **nearest-rank** percentile method.
Transaction Controller rows are excluded from endpoint totals to avoid double counting.

## Overall endpoint metrics

| Samples | Error % | Mean ms | p50 ms | p90 ms | p95 ms | p99 ms | Max ms | Samples/s |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 39502 | 0.0 | 4.281 | 4.0 | 5.0 | 6.0 | 9.0 | 583.0 | 43.9395 |

## Per-label metrics

| Label | Samples | Error % | Mean ms | p95 ms | p99 ms | Max ms | Samples/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `01_POST_register` | 13168 | 0.0 | 6.198 | 8.0 | 11.0 | 583.0 | 14.6472 |
| `02_GET_admin_users` | 13167 | 0.0 | 1.817 | 4.0 | 8.0 | 396.0 | 14.6544 |
| `03_DELETE_registered_user` | 13167 | 0.0 | 4.826 | 6.0 | 9.0 | 345.0 | 14.6558 |

## Response codes

```json
{
  "200": 39502
}
```
