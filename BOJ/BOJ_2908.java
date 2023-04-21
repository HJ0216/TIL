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
		
		int a = Integer.parseInt(st.nextToken());
		int b = Integer.parseInt(st.nextToken());

		List<Integer> listA = new ArrayList<>();
		List<Integer> listB = new ArrayList<>();
		
		listA.add((a%10));
		listA.add((a/10)%10);
		listA.add((a/100)%10);
		
		listB.add((b%10));
		listB.add((b/10)%10);
		listB.add((b/100)%10);
		
		if(listA.get(0)>listB.get(0)) {
			bw.write(listA.get(0) + "" + listA.get(1) + "" + listA.get(2));
		} else if(listA.get(0)<listB.get(0)) {
			bw.write(listB.get(0) + "" + listB.get(1) + "" + listB.get(2));
		} else {
			if(listA.get(1)>listB.get(1)) {
				bw.write(listA.get(0) + "" + listA.get(1) + "" + listA.get(2));				
			} else if(listA.get(1)<listB.get(1)) {
				bw.write(listB.get(0) + "" + listB.get(1) + "" + listB.get(2));				
			} else {
				if(listA.get(2)>listB.get(2)) {
					bw.write(listA.get(0) + "" + listA.get(1) + "" + listA.get(2));									
				} else {
					bw.write(listB.get(0) + "" + listB.get(1) + "" + listB.get(2));									
				}
			}
		}
		
		bw.flush();
		bw.close();
		
	}	
}
