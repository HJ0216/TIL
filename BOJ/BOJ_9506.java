import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

		int n;

		while((n = Integer.parseInt(br.readLine()))!=-1) {
			List<Integer> intList = new ArrayList<>();
			
			int sum=0;
			for(int i=1; i<n; i++) {
				if(n%i==0) {
					intList.add(i);
					sum += i;
				}
				
			}			
			if(sum==n) {
				bw.write(n + " = ");
				for(int j=0; j<intList.size(); j++) {
					bw.write(intList.get(j)+" ");
					if(j!=intList.size()-1) {
						bw.write("+ ");
					} else {
						bw.write("\n");
					}
				}
			} else {
				bw.write(n + " is NOT perfect.\n");
			}
		}
		bw.flush();
		bw.close();
	}

}
