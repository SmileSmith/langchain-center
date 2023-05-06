# 表格配置 Schema

## Schema配置项
```typescript
// 表格Schema的完整定义
interface Schema {{
  id?: string
  className?: string
  style?: React.CSSProperties
  innerClassName?: string
  innerStyle?: React.CSSProperties
  columns: Column[]
  bordered?: boolean
  showHeader?: boolean
  header?: HeaderOrFooter
  footer?: SchemaFooter
  // default: {{ size:'small', pageSize: 10, position: 'bottomRight' }}
  pagination?: Pagination
  size?: 'small' | 'middle' | 'large' | 'default'
  sticky?: boolean
  scroll?: Scroll
  rowSelection?: RowSelection
  rowDraggable?: boolean
  editable?: boolean
  tableLayout?: 'auto' | 'fixed'
  stripe?: boolean
  virtual?: boolean
  // default: 100
  rowHeight?: number
  rowKey?: string
  rowSlotKey?: string
  rowHeader?: HeaderOrFooter | boolean
  rowFooter?: HeaderOrFooter | boolean
  emptyText?: string
  subtable?: {{ dataSourceKey: string }} & Schema
}}
// columns列定义: `columns` 字段为一个由列描述对象组成的数组，数组的每个元素即列描述对象与列组件一一对应。
interface Column {{
  key: string
  title: string
  // 取数据的字段
  dataIndex: string | string[]
  dataTranslation?: FunctionString
  defaultValue?: string | number | boolean
  style?: React.CSSProperties
  hoverStyle?: React.CSSProperties
  rowHoverStyle?: React.CSSProperties
  columnHoverStyle?: React.CSSProperties
  width?: string | number
  // default: 'left'
  align?: Align
  // default: 'top'
  verticalAlign?: VerticalAlign
  description?: string
  // default: 'left'
  fixed?: 'left' | 'right' | boolean
  hidden?: boolean | FunctionString
  disable?: boolean | FunctionString
  editable?: boolean | FunctionString
  hidable?: boolean
  filters?: Filter[]
  defaultFilteredValue?: React.Key[]
  component: string
  options?: Record<string, unknown>
}}
interface HeaderOrFooter {{
  style?: React.CSSProperties
  elements?: Element[]
}}
interface Element {{
  type: 'html'
  html: string
}}
type Pagination = false|{{
  size?: 'small'|'default'
  pageSize?: number
  position?: 'topLeft'|'topCenter'|'topRight'|'bottomLeft'|'bottomCenter'|'bottomRight'
  showLessItems?: boolean
  showQuickJumper?: boolean
  showSizeChanger?: boolean
  pageSizeOptions?: string[]|number[]
  hideOnSinglePage?: boolean
  showTotal?: boolean|string
}}
interface Scroll {{
  x?: number|true|string
  y?: number|string
  scrollToFirstRowOnChange?: boolean
}}
type Align = 'left'|'center'|'right'
type VerticalAlign = 'top'|'middle'|'bottom'|'stretch'
type RowSelection = boolean|{{
  align?: Align
  verticalAlign?: VerticalAlign
}}
interface Filter = {{
  text: React.ReactNode
  value: string|number|boolean
}}
// 当传入FunctionString(脚本字符串)控制时，可通过 `props.record` 获取当前行数据，通过 `props.recordIndex` 获取当前行号，通过 `props.value` 获取当前单元格数据。例子：'return [2, 5, 7].includes(props.record.id)'
type FunctionString = string
```

dataIndex枚举值如下：'id', 'demoPic', 'name', 'startDate', 'endDate', 'dateRange', 'num', 'pictureUrl', 'description', 'status', 'price'

## schema示例
```json
{{
  "stripe": true,
  "columns": [
    {{
      "key": "id",
      "title": "id",
      "dataIndex": "id",
      "component": "text",
      "options": {{
        "mode": "single"
      }}
    }},
    {{
      "key": "mock_2",
      "title": "商品详情",
      "align": "center",
      "dataIndex": "description",
      "component": "text",
      "options": {{
        "mode": "single",
        "ellipsis": true
      }}
    }}
  ]
}}
```
