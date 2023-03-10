import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		
		Scanner scan = new Scanner(System.in);
		int a1 = scan.nextInt();
		int a2 = scan.nextInt();
		
		if(a1>a2) {System.out.println(">");}
		else if(a1<a2) {System.out.println("<");}
		else {System.out.println("==");}
		scan.close();
	}
}
