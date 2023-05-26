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

		List<Integer> list = new ArrayList<>();
		
		for(int i=0; i<9; i++) {
			int num=Integer.parseInt(br.readLine());
			list.add(num);
		}
		
		int max=0;
		for(int i=0; i<9; i++) {
			if(list.get(i)>max) {
				max=list.get(i);
			}
		}
		
		bw.write(max+"\n");
		bw.write((list.indexOf(max)+1)+"");
		bw.flush();
		bw.close();
	}
}
