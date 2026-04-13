`timescale 1ns / 1ps

module testbench;
    reg a, b, sel;
    wire out;
    wire expected_out;

    top_module dut(.a(a), .b(b), .sel(sel), .out(out));

    assign expected_out = sel ? b : a;

    integer total_samples = 0;
    integer mismatches = 0;

    task check;
        begin
            total_samples = total_samples + 1;
            if (out !== expected_out) begin
                mismatches = mismatches + 1;
                $display("MISMATCH at time %0t: a=%b b=%b sel=%b out=%b expected=%b",
                         $time, a, b, sel, out, expected_out);
            end
        end
    endtask

    initial begin
        a = 0; b = 0; sel = 0; #10; check;
        a = 0; b = 1; sel = 0; #10; check;
        a = 1; b = 0; sel = 0; #10; check;
        a = 1; b = 1; sel = 0; #10; check;
        a = 0; b = 0; sel = 1; #10; check;
        a = 0; b = 1; sel = 1; #10; check;
        a = 1; b = 0; sel = 1; #10; check;
        a = 1; b = 1; sel = 1; #10; check;

        $display("Hint: Total mismatched samples is %0d out of %0d samples", mismatches, total_samples);
        if (mismatches == 0) $display("ALL TESTS PASSED");
        else $display("SOME TESTS FAILED");
        $finish;
    end
endmodule
