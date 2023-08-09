import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.StringTokenizer;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		StringTokenizer st1 = new StringTokenizer(br.readLine(), " ");
		int top1 = Integer.parseInt(st1.nextToken());
		int bottom1 = Integer.parseInt(st1.nextToken());

		StringTokenizer st2 = new StringTokenizer(br.readLine(), " ");
		int top2 = Integer.parseInt(st2.nextToken());
		int bottom2 = Integer.parseInt(st2.nextToken());

		int top = top1 * bottom2 + top2 * bottom1;
		int bottom = bottom1 * bottom2;

		int gdc = getGCD(top, bottom);

		bw.write((top/gdc) + " " + (bottom/gdc));

		bw.flush();
		bw.close();
	}
	
    public static int getGCD(int p, int q) {
    	return q == 0 ? p : getGCD(q, p%q);
    }

}
