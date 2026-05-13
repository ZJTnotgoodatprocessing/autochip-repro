# v9 参考文献核验记录

> 日期：2026-05-13

## [s.n.] 处理结果

v8 报告错误声称 [s.n.] 为 0。经检查 PDF 和 bibs.bib，以下 4 条 `@inproceedings` 缺少 `publisher` 字段，在 GB/T 7714 格式下会生成 `[s.n.]`：

| # | BibKey | booktitle | 原因 | 处理 |
|---|--------|-----------|------|------|
| 1 | autochip | ML for Systems Workshop at NeurIPS | Workshop 论文，无正式出版者 | 保留 [s.n.]，如实说明 |
| 2 | chipchat | ML for Systems Workshop at NeurIPS | Workshop 论文，无正式出版者 | 保留 [s.n.]，如实说明 |
| 3 | autobench | ML for Systems Workshop at NeurIPS | Workshop 论文，无正式出版者 | 保留 [s.n.]，如实说明 |
| 4 | yosys | Austrochip Workshop | Workshop 论文，无正式出版者 | 保留 [s.n.]，如实说明 |

**说明**：以上 4 条均为 workshop 论文。NeurIPS 的 workshop 论文不由 Curran Associates 出版（仅主会论文由 Curran 出版），Austrochip Workshop 同样无正式出版社。为这些条目添加虚假 publisher 违反学术规范。因此保留 [s.n.]，不做虚假补充。

## 总参考文献数

编译后：**27 条**，0 BibTeX warning。其中 4 条 workshop 论文存在 [s.n.]。
