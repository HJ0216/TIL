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

		StringTokenizer st = new StringTokenizer(br.readLine(), " ");
		int n = Integer.parseInt(st.nextToken());
		int m = Integer.parseInt(st.nextToken());
		
		List<Integer> list = new ArrayList<>();
		
		
		for(int i=0; i<n; i++) {
			list.add(0);
		}
		
		for(int i=0; i<m; i++) {
			StringTokenizer st2 = new StringTokenizer(br.readLine(), " ");
			int a = Integer.parseInt(st2.nextToken())-1;
			int b = Integer.parseInt(st2.nextToken())-1;
			int c = Integer.parseInt(st2.nextToken());
			
			for(int j=a; j<=b; j++) {list.set(j, c);}	
		}
		
		for(int i :list) {
			bw.write(i + " ");
		}
		
		bw.flush();
		bw.close();
	}
}
