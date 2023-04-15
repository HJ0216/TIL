import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws IndexOutOfBoundsException, IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		StringTokenizer st = new StringTokenizer(br.readLine(), " ");
		int n = Integer.parseInt(st.nextToken());
		int m = Integer.parseInt(st.nextToken());
		
		List<Integer> list1 = new ArrayList<>();
		List<Integer> list2 = new ArrayList<>();
		for(int i=0; i<n; i++) {
			list1.add((i+1));
			list2.add((i+1));
		} // list[0] = 1, list[1] = 2, ..
		
		
		int sNum=0;
		int eNum=0;
		for(int i=0; i<m; i++){
			StringTokenizer st2 = new StringTokenizer(br.readLine(), " ");
			sNum = Integer.parseInt(st2.nextToken());
			eNum = Integer.parseInt(st2.nextToken());
			
			for(int j=0; j<(eNum-sNum+1); j++) {
				list1.set(sNum-1+j, list2.get((eNum-1-j)));

				if(j==(eNum-sNum)) {
					for(int k=0; k<n; k++) {
						list2.set(k, list1.get(k));
					}
				}
			}

		}
		
		for(int element : list1) {
			bw.write(element + " ");
		}
		
		bw.flush();
		bw.close();
		
	}
}
