public class IntMathHelper {
    int x;
    int y;

    public IntMathHelper() {
        this(0, 0);
    }

    public IntMathHelper(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int add() {
        return this.x + this.y;
    }

    public int sub() {
        return this.x - this.y;
    }

    public int mul() {
        return this.x * this.y;
    }

    public double div() {
        return ( this.x * 1.0 ) / this.y;
    }

}
