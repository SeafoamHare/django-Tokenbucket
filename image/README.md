## Pattern Oriented Software Design 2024 Fall Assignment

## Important Links
- [Course Link](http://140.124.181.100/yccheng/posd2024f)
- [Gitlab](http://140.124.181.100)
- [Jenkins](http://140.124.181.97:8080)
- [Microsoft Teams](https://teams.microsoft.com/l/team/19%3AoQBubdF152LO2WVrJMRHVX7rOx0wb_v4twMSorq8Va81%40thread.tacv2/conversations?groupId=f0cff185-d612-415d-8bf9-76ed37baeee0&tenantId=dfb5e216-2b8a-4b32-b1cb-e786a1095218)

- [Environment Setting Tutorial](environment_setting.md)

## Assignment List

* [Environment Setting](#environment_setting)
* [Assignment 1](#assignment-1): Due 9/15 23:59

## Environment Setting 

**Notice**: 
1. You should make sure Jenkins and GitLab hooks correctly before doing assignment 1. 
2. Please contact the TA before or during TA's office hours if you have any problems.

* [Environment Setting](./environment_setting.md)

## Assignment 1
**Deadline**: 23:59 on September 15, 2024.

**Notice**: 
1. **Complete the environment setting** before assignment 1.
2. If your code fails to compile on jenkins server, you'll get no point for the assignment. 

Here's [the code](http://140.124.181.100/course/posd2024f_ta/-/tree/assignment1_template_code) modified from the code written in class, please download and add them to your homework repository.

**Note: Each class in the sample file is the skeleton. You should finish implementation by yourself.**

For this Assignment, you'll solve the sorting shape problem below.
### Problem statement
** Review Problem 1 (Homework 1): sorting shapes**
A simple geometry application called _geo_ is needed to sort shapes such as triangles, circles, rectangles and others. As a command line application, _geo_ reads shapes from an input file, sorts the shapes by area or perimeter in increasing order or decreasing order, and write the result to an output file. For example,
```
geo input.txt output.txt area inc
```
sorts the shapes in file _input.txt_ in increasing order by area, and writes the result to the file _output.txt_. And
```
geo input.txt output.txt perimeter dec
```
sorts the shapes in file _input.txt_ in decreasing order by perimeter, and writes the result to the file _output.txt_.

### Specification
Please complete the given code to satisfy all the following conditions.

* Please implement shapes - `Circle`, `Triangle`, `Rectangle`.
	* Complete `area()`, `perimeter()`, and `toString()`.

	* The `toString()` method will return the format we've given in `input.txt`.

* Please implement the following class - `Sort`.

	* In the Sort class please complete "ByAreaAscending", "ByAreaDescending", "ByPerimeterAscending", and "ByPerimeterDescending".

	* **Don't use lambda in this assignment.**

* Please do exception handling if the shape can't be successfully created.(The excepton type of the TA's test will be **Exception** and throw `It's not a circle!`, `It's not a rectangle!`, `It's not a triangle!`)

* If the input shape can't be successfully created, just **ignore** and output the shapes which are correct.

* For each function/method, write at least one unit test for it.

* For the arguments in this project,
	* `args[0]` is the input file name,
	* `args[1]` is the output file name,
	* `args[2]` is the condition which you want to sort,
	* `args[3]` is the order which you want to sort.
	* If the input of `args[2]` or `args[3]` is invalid, just **ignore** and output the correct shapes. The order is the same as the input. _Updated 2024/09/10 22:52_
	* Hint:
	You can execute the program by the following command
	```
	mvn exec:java -Dexec.mainClass="org.ntutssl.shapes.Geo" -Dexec.args="test_data/input.txt test_data/output.txt {area inc}"
	```
	change ```area inc``` to `area dec`, `perimeter inc` or `perimeter dec`

* Please make your directory follow the following file structure:

```
├── pom.xml
├── src
│   ├── main
│   │   └── java
│   │       └── org
│   │           └── ntut
│   │               └── posd2024f
│   │               	└── shapes
│   │                   	├── Circle.java
│   │                   	├── Geo.java
│   │                   	├── InputOutput.java
│   │                   	├── Shape.java
│   │                   	├── Rectangle.java
│   │                   	├── Sort.java
│   │                   	└── Triangle.java
│   └── test
│       └── java
│           └── org
│               └── ntut
│                   └── posd2024f
│                   	└── shapes
│                       	├── CircleTest.java
│                       	├── RectangleTest.java
│                       	├── ShapeTest.java
│                       	├── SortTest.java
│                       	└── TriangleTest.java
└── test_data
    ├── input.txt
    └── output.txt
```
## Score
1. Unit tests written by yourself: 35%.
2. Unit tests written by TA: 35%.
3. The executable program: 30%.

## References
* [static class](https://www.geeksforgeeks.org/static-class-in-java/)

* [Comparator](https://docs.oracle.com/javase/8/docs/api/java/util/Comparator.html)

* [YC Cheng's blog about polygon](http://htsicpp.blogspot.com/2014/10/convex-polygon.html)

* [Oracle Java Document](https://docs.oracle.com/javase/8/docs/api/index.html)


