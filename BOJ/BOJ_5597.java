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

		List<Integer> list1 = new ArrayList<>();
		for(int i=0; i<30; i++) {
			list1.add(i+1);
		}
		
		List<Integer> list2 = new ArrayList<>();
		for(int i=0; i<28; i++) {
			list2.add(Integer.parseInt(br.readLine()));
		}


		for(int i=0; i<30; i++) {
			int j;
			for(j=0; j<28; j++) {
				if(list1.get(i)==list2.get(j)) {break;}
			}
			if(j==28){bw.append(String.valueOf(list1.get(i)) + "\n");}
		}
		
		bw.flush();
		bw.close();
		
	}
}
