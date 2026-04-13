`timescale 1ns / 1ps

module testbench;
    reg [2:0] in;
    wire [1:0] out;
    wire [1:0] expected_out;

    top_module dut(.in(in), .out(out));

    assign expected_out = in[0] + in[1] + in[2];

    integer total_samples = 0;
    integer mismatches = 0;

    task check;
        begin
            total_samples = total_samples + 1;
            if (out !== expected_out) begin
                mismatches = mismatches + 1;
                $display("MISMATCH at time %0t: in=%b out=%0d expected=%0d",
                         $time, in, out, expected_out);
            end
        end
    endtask

    integer i;
    initial begin
        // Exhaustive test: all 8 combinations
        for (i = 0; i < 8; i = i + 1) begin
            in = i[2:0]; #10; check;
        end

        $display("Hint: Total mismatched samples is %0d out of %0d samples", mismatches, total_samples);
        if (mismatches == 0) $display("ALL TESTS PASSED");
        else $display("SOME TESTS FAILED");
        $finish;
    end
endmodule
