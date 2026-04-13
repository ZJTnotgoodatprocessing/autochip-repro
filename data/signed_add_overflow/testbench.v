`timescale 1ns / 1ps

module testbench;
    reg [7:0] a, b;
    wire [7:0] sum;
    wire overflow;
    wire [7:0] expected_sum;
    wire expected_overflow;

    top_module dut(.a(a), .b(b), .sum(sum), .overflow(overflow));

    // Golden model
    assign expected_sum = a + b;
    assign expected_overflow = (a[7] == b[7]) && (expected_sum[7] != a[7]);

    integer total_samples = 0;
    integer mismatches = 0;

    task check;
        begin
            total_samples = total_samples + 1;
            if (sum !== expected_sum || overflow !== expected_overflow) begin
                mismatches = mismatches + 1;
                $display("MISMATCH at time %0t: a=%0d b=%0d sum=%0d(exp=%0d) overflow=%b(exp=%b)",
                         $time, $signed(a), $signed(b), $signed(sum), $signed(expected_sum),
                         overflow, expected_overflow);
            end
        end
    endtask

    initial begin
        // Basic cases: no overflow
        a = 8'd10;   b = 8'd20;   #10; check;  // 10+20=30
        a = 8'd0;    b = 8'd0;    #10; check;  // 0+0=0
        a = 8'd1;    b = -8'd1;   #10; check;  // 1+(-1)=0

        // Positive overflow cases
        a = 8'd100;  b = 8'd100;  #10; check;  // 100+100=200 -> overflow (>127)
        a = 8'd127;  b = 8'd1;    #10; check;  // 127+1 -> overflow
        a = 8'd64;   b = 8'd64;   #10; check;  // 64+64=128 -> overflow
        a = 8'd120;  b = 8'd10;   #10; check;  // 120+10=130 -> overflow

        // Negative overflow cases
        a = -8'd100; b = -8'd100; #10; check;  // -100+(-100)=-200 -> overflow (<-128)
        a = -8'd128; b = -8'd1;   #10; check;  // -128+(-1) -> overflow
        a = -8'd80;  b = -8'd80;  #10; check;  // -80+(-80)=-160 -> overflow

        // Mixed sign: never overflows
        a = 8'd127;  b = -8'd128; #10; check;  // 127+(-128)=-1
        a = -8'd1;   b = 8'd127;  #10; check;  // -1+127=126
        a = 8'd50;   b = -8'd30;  #10; check;  // 50+(-30)=20
        a = -8'd50;  b = 8'd30;   #10; check;  // -50+30=-20

        // Edge values
        a = 8'd127;  b = 8'd0;    #10; check;
        a = -8'd128; b = 8'd0;    #10; check;
        a = 8'd127;  b = -8'd127; #10; check;  // 127+(-127)=0
        a = -8'd128; b = 8'd127;  #10; check;  // -128+127=-1

        // Boundary overflow checks
        a = 8'd126;  b = 8'd1;    #10; check;  // 127, no overflow
        a = 8'd126;  b = 8'd2;    #10; check;  // 128 -> overflow
        a = -8'd127; b = -8'd1;   #10; check;  // -128, no overflow
        a = -8'd127; b = -8'd2;   #10; check;  // -129 -> overflow

        // Random-ish additional vectors
        a = 8'd55;   b = 8'd80;   #10; check;  // 135 -> overflow
        a = -8'd60;  b = -8'd70;  #10; check;  // -130 -> overflow
        a = 8'd33;   b = 8'd44;   #10; check;  // 77, no overflow
        a = -8'd33;  b = -8'd44;  #10; check;  // -77, no overflow

        $display("Hint: Total mismatched samples is %0d out of %0d samples", mismatches, total_samples);
        if (mismatches == 0) $display("ALL TESTS PASSED");
        else $display("SOME TESTS FAILED");
        $finish;
    end
endmodule
