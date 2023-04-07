import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;

public class Main {
	public static void main(String[] args) throws IndexOutOfBoundsException, IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		List<Integer> list = new ArrayList<>();
		for(int i=0; i<10; i++) {
			list.add(Integer.parseInt(br.readLine())%42);
		}
		
		int count = 0;
		for(int i=0; i<10; i++) {
			for(int j=i+1; j<10; j++) {
				if(list.get(i)==list.get(j)) {
					count++;
					break;}
			}
		}
		
		bw.write(String.valueOf(10-count));
		
		bw.flush();
		bw.close();
		
	}
}
