
import java.util.Scanner;

public class Main {
	
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		
		int a = scan.nextInt();
		int b = scan.nextInt();
		
		int i = a*(b%10);
		int i2 = a*((b/10)%10);
		int i3 = a*(b/100);
		
		System.out.println(i);
		System.out.println(i2);
		System.out.println(i3);
		System.out.println(i + i2*10 + i3*100);
		
		scan.close();
	}
	
}
