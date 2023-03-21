import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int a = scan.nextInt();
		
		List<Integer> list = new ArrayList<>();

		for(int i=0; i<a; i++) {
			int b = scan.nextInt();
			list.add(b);
		}

		int c = scan.nextInt();
		
		int count=0;
		for(int i=0; i<a; i++) {
			if(list.get(i)==c) {
				count++;
			}
		}
		
		System.out.println(count);
		
		scan.close();
	}
}
