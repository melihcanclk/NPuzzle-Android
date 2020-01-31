import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        NPuzzle npuzzle = new NPuzzle();

        Scanner scan = new Scanner(System.in);

        System.out.print("Enter X length of board:");
        int x = scan.nextInt();
        System.out.print("Enter Y length of board:");
        int y = scan.nextInt();
        npuzzle.setSize(x,y);
        System.out.println(npuzzle);

        scan.close();
    }
}