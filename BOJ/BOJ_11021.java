import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int t = scan.nextInt();
		
		List<Integer> list = new ArrayList<>();
		for(int i=0; i<t; i++) {
			int a = scan.nextInt();
			int b = scan.nextInt();
			list.add(a+b);
		}
		for(int i=1; i<=list.size(); i++) {
			System.out.println("Case #" + i + ": " + list.get(i-1) );
		}
	}
}
