# mermaid 语法示例

[官网](https://mermaid.js.org/)

[在线编辑器](https://mermaid-js.github.io/mermaid-live-editor/)


**流程图**
```mermaid
graph TD;
    A-->B
    A-->C;
    B-->D;
    C-->D;
```

<br><br>

**顺序图**
```mermaid
sequenceDiagram
	participant Alice
    participant Bob
    participant John
    Alice->>John: Hello John, how are you?
    loop Healthcheck
    	John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts <br/>prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
```

<br><br>

**甘特图**
```mermaid  
gantt  
    title A Gantt Diagram  
    dateFormat  YYYY-MM-DD  
    section Section  
    A task           :a1, 2014-01-01, 30d  
    Another task     :after a1  , 20d  
    section Another  
    Task in sec      :2014-01-12  , 12d  
    another task      : 24d  
```

<br>

```mermaid
gantt
dateFormat YYYY-MM-DD
title Adding GANTT diagram to mermaid
excludes weekdays 2014-01-10

section A section
Completed task: done, des1, 2014-01-06, 2014-01-08
Active task:active, des2, 2014-01-09, 3d
Future task: des3, after des2, 5d
Future task2: des4, after des3, 5d
```

<br><br>

**类图**

```mermaid
classDiagram
Class01 <|-- AveryLongClass: Cool
Class03 *-- Class04
Class05 o-- Class06
Class07 .. Class08
Class09 --> C2: Where am i?
Class09 --* C3
Class09 --|> Class07
Class07: equals()
Class07: Object[] elemeentData
Class01: size()
Class01: int chimp
Class01: int gorilla
Class08 <--> C2: Cool label
```

<br><br>

**状态图**

```mermaid
stateDiagram
[*] --> Still
Still --> [*]

Still --> Moving
Moving --> Still
Moving --> Crash
Crash --> [*]
```

<br><br>

**实体关系图**

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
```

<br><br>

**鱼骨图**

```mermaid
graph LR
    A[Christmas] -->|Get money| B(Go shopping)
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[Car]
```

<br><br>

**GIT图**

```mermaid
gitGraph:
<!-- options
{
	"nodeSpacing": 150,
	"nodeRadius": 10
}
end
commit
branch newbranch
checkout newbranch
commit
commit
checkout master
commit
commit
merge newbranch -->
```