/* 
 * Sample C Program for Lexical Analyzer Testing
 * This file contains various C language constructs
 */

// Structure definition
struct Point {
    int x;
    int y;
};

struct Student {
    char name[50];
    int id;
    float gpa;
    struct Point location;
};

// Enumeration
enum Color {
    RED,
    GREEN,
    BLUE,
    YELLOW = 10
};

// Global variables
int global_counter = 0;
const float GRAVITY = 9.81;

// Function prototypes
int factorial(int n);
void swap(int *a, int *b);
struct Point createPoint(int x, int y);
float calculateDistance(struct Point p1, struct Point p2);

/* 
 * Main function demonstrating various C features
 */
int main(void) {
    // Variable declarations
    int numbers[5] = {1, 2, 3, 4, 5};
    char message[] = "Hello, World!";
    float result = 0.0;
    struct Student student1;
    
    // Assignment and arithmetic operations
    int a = 10, b = 20;
    int sum = a + b;
    int diff = a - b;
    int product = a * b;
    float quotient = (float)a / b;
    int remainder = a % 3;
    
    // Relational and logical operators
    if (a < b && b > 0) {
        result = 1.0;
    } else if (a == b || a > 100) {
        result = 2.0;
    } else {
        result = 3.0;
    }
    
    // Increment and decrement
    a++;
    ++b;
    a--;
    --b;
    
    // Compound assignment
    a += 5;
    b -= 3;
    a *= 2;
    b /= 2;
    
    // Bitwise operations
    int bits = 0xFF;
    bits = bits & 0x0F;
    bits = bits | 0x10;
    bits = bits ^ 0x05;
    bits = ~bits;
    bits = bits << 2;
    bits = bits >> 1;
    
    // For loop
    for (int i = 0; i < 5; i++) {
        numbers[i] = numbers[i] * 2;
    }
    
    // While loop
    int count = 0;
    while (count < 10) {
        count++;
        if (count == 5) {
            continue;
        }
        if (count == 8) {
            break;
        }
    }
    
    // Do-while loop
    do {
        count--;
    } while (count > 0);
    
    // Switch statement
    enum Color color = RED;
    switch (color) {
        case RED:
            result = 10.0;
            break;
        case GREEN:
            result = 20.0;
            break;
        case BLUE:
            result = 30.0;
            break;
        default:
            result = 0.0;
    }
    
    // Structure usage
    student1.id = 12345;
    student1.gpa = 3.85;
    student1.name[0] = 'J';
    student1.name[1] = 'o';
    student1.name[2] = 'h';
    student1.name[3] = 'n';
    student1.name[4] = '\0';
    
    // Pointer operations
    int *ptr = &a;
    *ptr = 100;
    int **double_ptr = &ptr;
    
    // Function calls
    int fact = factorial(5);
    swap(&a, &b);
    struct Point p1 = createPoint(3, 4);
    struct Point p2 = createPoint(6, 8);
    float distance = calculateDistance(p1, p2);
    
    // Ternary operator
    int max = (a > b) ? a : b;
    
    // Array of structures
    struct Point points[3];
    points[0] = createPoint(1, 1);
    points[1] = createPoint(2, 2);
    points[2] = createPoint(3, 3);
    
    // String operations
    char str1[20] = "Test";
    char str2[20] = "String";
    
    // Comments in different styles
    /* Multi-line
       comment example */
    // Single line comment
    
    return 0;
}

// Function to calculate factorial
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// Function to swap two integers using pointers
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Function to create a Point structure
struct Point createPoint(int x, int y) {
    struct Point p;
    p.x = x;
    p.y = y;
    return p;
}

// Function to calculate distance between two points
float calculateDistance(struct Point p1, struct Point p2) {
    int dx = p2.x - p1.x;
    int dy = p2.y - p1.y;
    float distance = (dx * dx) + (dy * dy);
    return distance; // Note: should use sqrt, simplified for testing
}