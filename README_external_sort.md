# 作业：超大二进制 int32 文件外部排序

## 文件

- `external_int32_sort.py`：主程序，完成外部排序。
- `make_test_int32_file.py`：生成测试用 int32 二进制文件。
- `check_int32_sorted.py`：检查排序结果是否正确。

## 运行主程序

```bash
python3 external_int32_sort.py input.bin 1000000
```

参数说明：

1. `input.bin`：无文件头的二进制文件，内容是连续的 32 位有符号整数。
2. `1000000`：允许同时加载进内存的整数数量。

程序会在源文件同目录生成：

```text
input_sorted.bin
```

## 算法说明

程序使用外部归并排序：

1. 按内存限制把大文件切成多个临时块。
2. 使用 `multiprocessing.Pool` 调用所有 CPU 核心并行排序这些块。
3. 把每个已排序块写入临时文件。
4. 使用堆 `heapq` 进行多路归并，生成最终有序文件。
5. 删除临时文件。

时间复杂度不超过：

```text
O(n log n)
```

硬盘空间要求：需要足够空间保存临时块文件。

## 测试示例

生成测试文件：

```bash
python3 make_test_int32_file.py test.bin 50000
```

排序：

```bash
python3 external_int32_sort.py test.bin 5000
```

检查结果：

```bash
python3 check_int32_sorted.py test_sorted.bin
```
