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

		List<Integer> list = new ArrayList<>();
		for(int i=0; i<5; i++) {
			list.add(Integer.parseInt(br.readLine()));
		}
		
		int sum=0;
		for(int i=0; i<list.size(); i++) {
			sum += list.get(i);
		}

		int avg=sum/list.size();
		
		bw.write(avg + "\n");
		
		list.sort(Comparator.naturalOrder());
		
		bw.write(list.get(2)+"");
		
		bw.flush();
		bw.close();
		
	}	
}
