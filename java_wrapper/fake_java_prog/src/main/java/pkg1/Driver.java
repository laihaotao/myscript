public class Driver {

    public static void main(String[] args) {
        IntMathHelper math = new IntMathHelper(1, 2);

        int addRes = math.add();
        int subRes = math.sub();
        int mulRes = math.mul();
        double divRes = math.div();

        System.out.println(addRes);
        System.out.println(subRes);
        System.out.println(mulRes);
        System.out.println(divRes);
    }

}
