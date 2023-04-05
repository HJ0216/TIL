import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int total = Integer.parseInt(br.readLine());
		
		List<Double> list = new ArrayList<>();
		
		StringTokenizer st = new StringTokenizer(br.readLine(), " ");
		
		for(int i=0; i<total; i++) {
			double num=Double.parseDouble(st.nextToken());
			list.add(num);
		}
		
		double max=0;
		for(int i=0; i<total; i++) {
			if(list.get(i)>=max) {
				max=list.get(i);
			}
		}
		
		double sum = 0;
		
		for(int i=0; i<total; i++) {
			list.set(i, (list.get(i)/max)*100);
			sum += list.get(i);
		}
		
		bw.write((sum/total)+"");
		bw.flush();
		bw.close();
	}
}
