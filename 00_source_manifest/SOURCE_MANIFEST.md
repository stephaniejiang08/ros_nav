# Source Manifest

Audit time: `2026-08-03T11:04:37+08:00`

Scope: source material used for the Windows-only document and source audit. Original files under `D:\cornerstone\技术文档` were read and hashed but were not modified. Files under `02_robot_vendor\extracted` are byte-for-byte extraction results from the composite robot ZIP.

| Role | Actual path | Size (bytes) | SHA256 | Status |
|---|---|---:|---|---|
| Linker Hand L6 product manual | `D:\cornerstone\技术文档\Linker  Hand L6 产品手册 20260402.pdf` | 1,390,990 | `E058FAD2391862882DF03FAFD656C8B2036131127E88C3C0A18141C036160E6D` | PASS |
| Linker Hand product catalog (secondary cross-check) | `D:\cornerstone\技术文档\灵心巧手产品手册20260707-中.pdf` | 5,882,453 | `2D6D8D57626F62D9D3630A0DDAAEB110AA5897EA14058603C38830C2502E5375` | PASS |
| Composite robot source archive | `D:\cornerstone\技术文档\哈工大（合肥）创新研究院复合机器人.zip` | 165,459,084 | `BDC113204CCC32A83C50D640D16F54DB1B41C2CC451DD5BD32A80100BCC55629` | PASS |
| Embedded Julab Mini archive | `D:\cornerstone\codex\linkerhand_composite_robot\02_robot_vendor\extracted\julab_mini-master-2.zip` | 133,061,517 | `BDD015EC5939AD704D37CE5575D94D397AB9924059CA623A421AE90098746F18` | PASS |
| Julab Mini manual | `D:\cornerstone\codex\linkerhand_composite_robot\02_robot_vendor\extracted\julab_mini-master-2\julab_mini-master\Julab mini使用说明书与快速入门手册V1.1.docx` | 6,625,161 | `57D18B74E2733726219F8CA2A2BBFD21F56CD9BA3722F351A8958A1037DC336C` | PASS |
| Sparrow Pro420 manual | `D:\cornerstone\codex\linkerhand_composite_robot\02_robot_vendor\extracted\灵雀Sparrow Pro420使用说明书与快速入门手册V2.0(11-5).pdf` | 3,188,079 | `D153C5ECF3816AB359B893ED93AFD9E8EE27CF410FF78F035DB79BBA07F13FF6` | PASS |
| Linux and ROS student guide bundled by robot vendor | `D:\cornerstone\codex\linkerhand_composite_robot\02_robot_vendor\extracted\２－Tonan　Linux＆ROS入门指导（学生版）.pdf` | 1,472,172 | `4BF34B841D2B535CDA528C19B7E9725B833B1F90290F697FA145A16058F2DE20` | PASS |
| MobaXterm installer archive bundled by robot vendor | `D:\cornerstone\codex\linkerhand_composite_robot\02_robot_vendor\extracted\MobaXterm_Installer_v20.1.zip` | 27,567,360 | `39AB11CA5BD68690D1AD39EB0782FC05AD4598E42B993FADA99658D2E3DBEA9F` | QUARANTINED / NOT_EXECUTED |

## Extraction record

- The composite robot ZIP contains six top-level entries.
- It was extracted to `D:\cornerstone\codex\linkerhand_composite_robot\02_robot_vendor\extracted`.
- `julab_mini-master-2.zip` was additionally extracted to `02_robot_vendor\extracted\julab_mini-master-2`.
- The nested Julab extraction contained 2,224 filesystem items at extraction time.
- No EXE, installer, shell script, Python demo, ROS launch file, ROS node, or hardware-control program was executed.
- The MobaXterm archive was retained only as a hashed vendor-supplied artifact and was not opened or run.

## Provenance distinction

The outer composite robot ZIP bundles two different product documentation sets:

1. `Julab Mini`: a dedicated DOCX manual plus ROS1 source tree.
2. `Sparrow Pro420`: a separate PDF manual describing a 6-axis INNFOS arm configuration.

These are not treated as the same robot model. The physical robot actually owned by the user remains `UNKNOWN` pending inspection of its nameplate and configuration.
