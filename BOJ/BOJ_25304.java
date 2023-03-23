import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int X = scan.nextInt();
		int N = scan.nextInt();

		int a, b;
		int sum=0;
		for(int i=0; i<N; i++) {
			a = scan.nextInt();
			b = scan.nextInt();
			sum += (a*b);
		}
		if(sum==X) {System.out.println("Yes");}
		else {System.out.println("No");}
		
		scan.close();
	}
}
