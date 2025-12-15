# Data Dictionary

This data dictionary describes measurement units and special codes used for geochemical element concentration fields.

---

## PCT (Percentage)

**Applies to:**  
All columns named using the convention `element_PCT` (e.g. `AG_PCT`)

| Possible Code | Description |
|--------------|-------------|
| `-9998` to `0` | Percentage (PCT) values below 0 (excluding `-9999`) indicate that the concentration is below the detection limit of the available technology |
| `-9999` | Represents a **NULL** value for elements that have not been analysed in a sample |
| `0` to `999,999.99` | Valid percentage values. Positive values indicate that the element concentration is high enough to be detected by the available measurement technology |

---

## PPB (Parts Per Billion)

**Applies to:**  
All columns named using the convention `element_PPB` (e.g. `AG_PPB`)

Percent, parts per million (PPM), and parts per billion (PPB) values that fall below 0 into negative values (excluding `-9999`) demonstrate that the concentration is below the detection limit of the available technology.

| Possible Code | Description |
|--------------|-------------|
| `-9998` to `0` | PPB values below 0 (excluding `-9999`) indicate concentrations below the detection limit |
| `-9999` | Represents a **NULL** value for elements that have not been analysed in a sample |
| `0` to `999,999.99` | Valid PPB values. Positive values indicate detectable element concentrations |

---

## PPM (Parts Per Million)

**Applies to:**  
All columns named using the convention `element_PPM` (e.g. `AG_PPM`)

Percent, parts per million (PPM), and parts per billion (PPB) values that fall below 0 into negative values (excluding `-9999`) demonstrate that the concentration is below the detection limit of the available technology.

| Possible Code | Description |
|--------------|-------------|
| `-9998` to `0` | PPM values below 0 (excluding `-9999`) indicate concentrations below the detection limit |
| `-9999` | Represents a **NULL** value for elements that have not been analysed in a sample |
| `0` to `999,999` | Valid PPM values. Positive values indicate detectable element concentrations |

---

## PPT (Parts Per Trillion)

**Applies to:**  
All columns named using the convention `element_PPT` (e.g. `AG_PPT`)

| Possible Code | Description |
|--------------|-------------|
| `-9998` to `0` | PPT values below 0 (excluding `-9999`) indicate concentrations below the detection limit of the available technology |
| `-9999` | Represents a **NULL** value for elements that have not been analysed in a sample |
| `0` to `999,999.99` | Valid PPT values. Positive values indicate that the element concentration is high enough to be detected by the available measurement technology |

---

## Notes

- `-9999` is consistently used across all units to represent **missing or unanalysed values**
- Negative values other than `-9999` indicate **below detection limit (BDL)** rather than true zero concentration
- Column naming convention:  
