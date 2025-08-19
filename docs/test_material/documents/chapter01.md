# 第1章: プログラミングの基礎

プログラミングの基本概念を学び、様々なMarkdown要素をテストします。

## プログラミングとは

プログラミングとは、コンピュータに対する**命令**を記述することです。

> プログラムとは、料理のレシピのようなもの。
> 材料（データ）と手順（アルゴリズム）を組み合わせて、
> 目的の結果を得るための指示書です。
> 

---

## プログラミング言語の種類

=== "Python"
    ```python
    # Pythonの例
    def hello():
        print("Hello, World!")

    hello()
    ```


=== "C言語"
    ```c
    // C言語の例
    #include <stdio.h>

    int main() {
        printf("Hello, World!\n");
        return 0;
    }
    ```


=== "JavaScript"
    ```javascript
    // JavaScriptの例
    function hello() {
        console.log("Hello, World!");
    }

    hello();
    ```


<iframe src="../../tables/language_comparison.html" width="100%"  style="border: 1px solid #ddd; border-radius: 4px;" scrolling="no" class="auto-height-iframe"></iframe>

## 基本的なプログラム構造

!!! note "重要な概念"
    すべてのプログラムは「順次」「分岐」「反復」の3つの基本構造で構成されます。

```python
# 順次処理の例
a = 10
b = 20
c = a + b
print(f"{a} + {b} = {c}")

```

!!! success "実行結果"
    ```
    10 + 20 = 30
    ```
