import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.math.BigInteger;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws Exception {
			BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
			BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

			while(true) {

				StringTokenizer st = new StringTokenizer(br.readLine());
				
				int a1 = Integer.parseInt(st.nextToken());
				int a2 = Integer.parseInt(st.nextToken());
				int a3 = Integer.parseInt(st.nextToken());

				if(a1==0 && a2==0 && a3==0) {
					break;
				}
				
				if((a1>a2 && a1>a3) && ((a2+a3)<=a1)) {
					bw.write("Invalid\n");
				} else if((a2>a1 && a2>a3) && ((a1+a3)<=a2)) {
					bw.write("Invalid\n");				
				} else if((a3>a1 && a3>a2) && ((a1+a2)<=a3)) {
					bw.write("Invalid\n");
				} else {

					if(a1==a2 && a2==a3) {
						bw.write("Equilateral\n");
					} else if((a1==a2) &&  a2!=a3) {
						bw.write("Isosceles\n");
					} else if((a1==a3) &&  a2!=a3) {
						bw.write("Isosceles\n");
					} else if((a2==a3) &&  a2!=a1) {
						bw.write("Isosceles\n");
					} else {
						bw.write("Scalene\n");
					}				
					
				}
								
			}
						
			bw.flush();
			bw.close();
			
	}
}
