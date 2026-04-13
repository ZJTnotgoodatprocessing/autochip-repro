`timescale 1ns / 1ps

module testbench;
    reg in;
    wire out;
    wire expected_out;

    // DUT
    top_module dut(.in(in), .out(out));

    // Reference model
    assign expected_out = in;

    integer total_samples = 0;
    integer mismatches = 0;

    task check;
        begin
            total_samples = total_samples + 1;
            if (out !== expected_out) begin
                mismatches = mismatches + 1;
                $display("MISMATCH at time %0t: in=%b, out=%b, expected=%b",
                         $time, in, out, expected_out);
            end
        end
    endtask

    initial begin
        // Test vector 1
        in = 0; #10; check;
        // Test vector 2
        in = 1; #10; check;
        // Test vector 3
        in = 0; #10; check;
        // Test vector 4
        in = 1; #10; check;

        $display("Hint: Total mismatched samples is %0d out of %0d samples", mismatches, total_samples);

        if (mismatches == 0)
            $display("ALL TESTS PASSED");
        else
            $display("SOME TESTS FAILED");

        $finish;
    end
endmodule
