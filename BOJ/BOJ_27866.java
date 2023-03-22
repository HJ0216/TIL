import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		String a = scan.next();
		int b = scan.nextInt();
		
		System.out.println(a.substring(b-1, b));
		
		scan.close();
	}
}
