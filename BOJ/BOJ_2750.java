import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Main {
	public static void main(String[] args) throws IOException{
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		
		List<Integer> list = new ArrayList<>();
		
		int n = Integer.parseInt(br.readLine());
		for(int i=0; i<n;i++) {
			int a = Integer.parseInt(br.readLine());
			list.add(a);
		}
		list.sort(Comparator.naturalOrder());
		for(int i : list) System.out.println(i);

	}
}
