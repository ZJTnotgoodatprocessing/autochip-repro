`timescale 1ns / 1ps

module testbench;
    reg [7:0] a, b;
    wire [7:0] sum;
    wire [7:0] expected_sum;

    top_module dut(.a(a), .b(b), .sum(sum));

    assign expected_sum = a + b;

    integer total_samples = 0;
    integer mismatches = 0;

    task check;
        begin
            total_samples = total_samples + 1;
            if (sum !== expected_sum) begin
                mismatches = mismatches + 1;
                $display("MISMATCH at time %0t: a=%0d b=%0d sum=%0d expected=%0d",
                         $time, a, b, sum, expected_sum);
            end
        end
    endtask

    initial begin
        a = 8'd0;   b = 8'd0;   #10; check;
        a = 8'd1;   b = 8'd1;   #10; check;
        a = 8'd100; b = 8'd55;  #10; check;
        a = 8'd255; b = 8'd1;   #10; check;  // overflow: 0
        a = 8'd127; b = 8'd128; #10; check;  // overflow: 255
        a = 8'd200; b = 8'd200; #10; check;  // overflow: 144
        a = 8'd15;  b = 8'd240; #10; check;
        a = 8'd0;   b = 8'd255; #10; check;

        $display("Hint: Total mismatched samples is %0d out of %0d samples", mismatches, total_samples);
        if (mismatches == 0) $display("ALL TESTS PASSED");
        else $display("SOME TESTS FAILED");
        $finish;
    end
endmodule
