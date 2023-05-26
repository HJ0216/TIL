import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Main {
	public static void main(String[] args) throws IOException {		
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int n = Integer.parseInt(br.readLine());
		
		List<Integer> list = new ArrayList<>();
		while(true) {
			list.add(n%10);
			n = n/10;
			if(n==0) {break;}
		}
		
		list.sort(Comparator.reverseOrder());

		for(int i : list) {
			bw.write(i+"");			
		}
		
		bw.flush();
		bw.close();

	}		
}
