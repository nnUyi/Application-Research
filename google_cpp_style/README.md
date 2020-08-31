### vs code配置google代码风格
- 编辑器：vs code
- 插件：clang-format
- setting.json配置
```
{
    "editor.formatOnSave": true,
    "C_Cpp.updateChannel": "Insiders",
    "C_Cpp.clang_format_fallbackStyle": "Google",
    "C_Cpp.clang_format_style": "{ BasedOnStyle: Google, UseTab: Never, IndentWidth: 4, TabWidth: 4, AllowShortIfStatementsOnASingleLine: false, IndentCaseLabels: false, ColumnLimit: 0, AccessModifierOffset: -4, NamespaceIndentation: All }",
}
```
- 其他配置
```
  1. 将vs code的tab改为spaces
  2. loading
```
