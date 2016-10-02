import requests
import json
url = 'http://localhost:8080'
payload = "0.111987 0.001400 0.044404 0.023525 -0.044391 -0.082019 0.007066 0.019991 0.048768 0.029386 0.026322 0.024690 -0.021897 -0.043293 0.052737 -0.066481 0.006574 -0.055623 0.008939 -0.055128 -0.011399 -0.046891 0.057110 -0.024088 0.010818 0.064521 -0.099944 -0.035461 -0.015384 0.085665 -0.027101 -0.003697 -0.027723 0.021714 0.010818 -0.037462 -0.009313 0.024412 -0.072062 -0.023311 -0.049743 -0.124300 -0.040216 -0.034846 0.027103 -0.015163 0.051258 0.047012 -0.040567 0.030994 0.026976 -0.026490 -0.041720 -0.025279 -0.006913 0.014789 0.022421 0.010290 -0.054913 -0.009846 0.040649 -0.058565 -0.005632 -0.012442 -0.115684 -0.058419 0.021041 0.029457 0.014664 0.046026 -0.035767 0.048482 0.030120 -0.153292 0.050561 0.041402 -0.021651 0.038099 -0.025233 0.046260 -0.046255 0.077816 -0.083272 0.076878 0.100838 -0.033758 -0.047707 0.106306 -0.015670 -0.039829 0.139179 -0.055506 -0.130446 0.016743 -0.006882 0.006688 0.034877 0.048166 -0.163734 0.021808 -0.112625 -0.043213 -0.111943 -0.043627 -0.046874 0.038438 -0.021697 -0.001656 0.000660 -0.022249 0.009600 -0.037927 -0.114139 0.014313 -0.059427 -0.035085 -0.010055 0.044322 0.066665 -0.034704 -0.012636 -0.026514 0.001406 -0.077275 -0.013990 -0.017960 -0.037027 -0.045747 0.008965 0.035348 0.021281 0.031494 -0.005266 -0.008294 0.060380 -0.070884 -0.033593 0.010872 -0.002612 -0.103069 -0.055174 -0.046842 -0.049146 0.071552 -0.066019 0.043843 -0.113383 0.026797 0.051100 -0.085178 0.021758 0.006994 -0.043789 -0.012446 0.032259 -0.019852 0.015232 0.017434 -0.059360 -0.038529 0.014263 -0.094530 0.087641 0.014802 0.030447 0.049784 -0.071737 0.045624 -0.021961 0.016701 0.032051 0.007391 0.005345 0.007401 -0.022062 0.087973 0.023443 0.005064 0.041627 0.101813 -0.003917 -0.042699 -0.016017 -0.031803 0.018824 0.062465 0.035427 -0.026798 -0.018926 -0.023950 -0.023750 -0.021403 0.024362 0.008704 -0.034007 0.027825 -0.015776 -0.077436 0.093188 0.011003 0.015442 -0.006820 -0.032026 -0.017396 -0.064338 0.063057 -0.046229 0.061333 -0.129215 -0.083131 0.000011 -0.020624 0.039127 -0.065000 -0.024466 0.033087 0.030190 0.015782 0.016186 0.006375 0.046952 -0.017897 -0.001584 0.052792 -0.071909 -0.044242 -0.053708 0.064342 0.016620 0.096638 0.029160 -0.057666 0.004943 0.030618 0.014888 -0.094769 -0.054888 -0.045424 0.020546 0.041579 -0.025835 -0.039190 -0.047592 -0.004652 -0.011346 0.006134 0.009540 -0.009940 -0.017188 -0.021083 -0.047850 -0.041900 0.018297 0.030469 0.030737 -0.059558 0.004698 -0.024823 0.012955 0.038354 0.002201 -0.044818 0.028335 -0.152867 0.100240 -0.008111 -0.045790 0.021426 -0.055501 0.020748 -0.069998 0.070015 0.001222 0.069115 -0.008333 -0.005155 0.101576 0.089636 0.019908 -0.057125 0.041775 0.012129 -0.053018 0.016542 0.044840 -0.019653 -0.021268 -0.069894 -0.038134 0.013845 0.044806 -0.007400 0.029223 -0.026205 0.011703 0.035451 -0.001330 -0.003212 -0.056446 0.054202 -0.048750 -0.008341 -0.060584 0.052153 -0.047513 0.055814 0.006128 0.031157 -0.016179 0.039659 -0.124834 0.026563 -0.003410 0.135905 -0.003532 -0.009278 0.041228 0.082354 0.011508 0.062632 -0.025104 -0.045728 -0.056211 0.056752 -0.010509 -0.070009 0.059934 -0.016807 -0.008599 0.006556 0.000460 0.033557 0.028679 0.008663 -0.049899 -0.046774 -0.020490 -0.057981 -0.008006 0.014869 0.084218 -0.113326 -0.005987 0.026133 -0.090607 0.039201 0.001658 0.056044 -0.005552 -0.014911 -0.024744 0.044703 -0.046602 -0.103550 0.044867 -0.025888 -0.003699 -0.009445 -0.003075 0.025062 0.023740 -0.036234 0.053762 0.004945 0.012090 0.039952 0.048680 -0.008632 -0.014297 -0.039463 0.047424 0.022319 0.032710 0.014709 0.063721 0.020335 -0.055133 0.018358 0.095600 -0.028090 -0.038839 0.062659 0.131791 -0.048879 -0.028151 -0.086634 0.016640 0.077616 0.049277 -0.008302 0.103035 -0.062535 0.049605 -0.004699 0.029178 0.018516 -0.042991 0.018496 -0.086058 0.037404"
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.text.split('\n')