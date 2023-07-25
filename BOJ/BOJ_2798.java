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
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		
		StringTokenizer st1 = new StringTokenizer(br.readLine(), " ");
		int CNT = Integer.parseInt(st1.nextToken());
		int M = Integer.parseInt(st1.nextToken());		
		
		StringTokenizer st2 = new StringTokenizer(br.readLine(), " ");

		List<Integer> intList = new ArrayList<>();
		while(st2.hasMoreTokens()) {
			intList.add(Integer.parseInt(st2.nextToken()));
		}
		
		int result = 0;
		for(int i=0; i<intList.size()-2; i++) {
			for(int j=i+1; j<intList.size()-1; j++) {
				for(int k=j+1; k<intList.size(); k++) {
					int sum = intList.get(i)+intList.get(j)+intList.get(k);
					if(sum<=M) {
						result = (result <= sum) ? sum : result;
					}
				}
			}
			
		}

		bw.write(result + "");
		
		bw.flush();
		bw.close();
		
	}
	
}
