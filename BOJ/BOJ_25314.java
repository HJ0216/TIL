import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int N = scan.nextInt();

		List<String> list = new ArrayList<>();
		
		for(int i=0; i<N/4; i++) {
			list.add("long ");
		}
		list.add("int");
		
		for(String data : list) {
			System.out.print(data);
		}
		
		scan.close();
	}
}
