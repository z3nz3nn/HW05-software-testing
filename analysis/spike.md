# JTL analysis: 23127373_Spike_20260814.jtl

Generated from the raw CSV JTL using the **nearest-rank** percentile method.
Transaction Controller rows are excluded from endpoint totals to avoid double counting.

## Overall endpoint metrics

| Samples | Error % | Mean ms | p50 ms | p90 ms | p95 ms | p99 ms | Max ms | Samples/s |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 67818 | 0.0 | 27.255 | 6.0 | 91.0 | 104.0 | 124.0 | 283.0 | 161.8688 |

## Per-label metrics

| Label | Samples | Error % | Mean ms | p95 ms | p99 ms | Max ms | Samples/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `01_POST_register` | 22613 | 0.0 | 28.786 | 107.0 | 129.0 | 283.0 | 53.9744 |
| `02_GET_admin_users` | 22608 | 0.0 | 25.068 | 100.0 | 121.0 | 177.0 | 54.0189 |
| `03_DELETE_registered_user` | 22597 | 0.0 | 27.91 | 104.0 | 122.0 | 162.0 | 54.0031 |

## Response codes

```json
{
  "200": 67818
}
```
