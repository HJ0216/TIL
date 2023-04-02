import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws IOException{
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		StringTokenizer st = new StringTokenizer(br.readLine());

		int n = Integer.parseInt(st.nextToken());

		List<Integer> list = new ArrayList<>();
		
		
		st = new StringTokenizer(br.readLine());
		for(int i=0; i<n; i++) {
			int a = Integer.parseInt(st.nextToken());
			list.add(a);
		}
		
		list.sort(Comparator.naturalOrder());
		bw.write(list.get(0)+" ");
		bw.write(list.get(n-1)+" ");
		
		bw.flush();
		bw.close();
	}
}
