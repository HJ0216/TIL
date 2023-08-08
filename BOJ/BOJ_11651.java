import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.StringTokenizer;
public class Main {
	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
    
		int num = Integer.parseInt(br.readLine());
		int[][] intArrXY = new int[num][2];
    
		for (int i = 0; i < num; i++) {
			StringTokenizer st = new StringTokenizer(br.readLine(), " ");
			int a = Integer.parseInt(st.nextToken());
			int b = Integer.parseInt(st.nextToken());
			intArrXY[i][0] = a;
			intArrXY[i][1] = b;
		}
    
		Arrays.sort(intArrXY, new Comparator<int[]>() {
			@Override
			public int compare(int[] o1, int[] o2) {
				return o1[1] != o2[1] ? o1[1] - o2[1] : o1[0] - o2[0];
			}
		});
    
		for (int i = 0; i < num; i++) {
			bw.write(intArrXY[i][0] + " " + intArrXY[i][1] + "\n");
		}
    
		bw.flush();
		bw.close();
	}
}
