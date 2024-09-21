package mybankcalculator;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.DecimalFormat;

public class BC {
    
    public static void main(String[] args) {
        // 프레임 생성
        JFrame frame = new JFrame("적금 이자 계산기");
        frame.setSize(650, 400);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(null);
        
        // 글꼴 설정
        Font font = new Font("Dialog", Font.PLAIN, 14); // 기본 글꼴 크기 17로 설정

        // 입력 라벨 및 텍스트 필드 (매달 납입금액)
        JLabel monthlyLabel = new JLabel("매달 납입금액 (₩):");
        monthlyLabel.setBounds(50, 30, 150, 30);
        monthlyLabel.setFont(font);
        frame.add(monthlyLabel);

        JTextField monthlyField = new JTextField();
        monthlyField.setBounds(200, 30, 200, 30);
        monthlyField.setFont(font);
        frame.add(monthlyField);
        
        // 입력 라벨 및 텍스트 필드 (이율)
        JLabel rateLabel = new JLabel("이율 (%):");
        rateLabel.setBounds(50, 70, 150, 30);
        rateLabel.setFont(font);
        frame.add(rateLabel);
        
        JTextField rateField = new JTextField();
        rateField.setBounds(200, 70, 200, 30);
        rateField.setFont(font);
        frame.add(rateField);

        // 입력 라벨 및 텍스트 필드 (기간)
        JLabel monthsLabel = new JLabel("기간 (개월):");
        monthsLabel.setBounds(50, 110, 150, 30);
        monthsLabel.setFont(font);
        frame.add(monthsLabel);

        JTextField monthsField = new JTextField();
        monthsField.setBounds(200, 110, 200, 30);
        monthsField.setFont(font);
        frame.add(monthsField);
        
        // 결과 라벨
        JLabel resultLabel = new JLabel("결과:");
        resultLabel.setBounds(50, 210, 400, 30);
        resultLabel.setFont(font);
        frame.add(resultLabel);

        // 계산 버튼
        JButton calculateButton = new JButton("계산하기");
        calculateButton.setBounds(200, 160, 100, 30);
        calculateButton.setFont(font);
        frame.add(calculateButton);
        
        // 단리/복리 선택 체크박스
        JCheckBox compoundCheckBox = new JCheckBox("복리로 계산");
        compoundCheckBox.setBounds(50, 160, 150, 30);
        compoundCheckBox.setFont(font);
        frame.add(compoundCheckBox);
        
        // 버튼 클릭 이벤트
        calculateButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    // 입력값 가져오기
                    double monthlyPayment = Double.parseDouble(monthlyField.getText());
                    double annualRate = Double.parseDouble(rateField.getText()) / 100;
                    int months = Integer.parseInt(monthsField.getText());
                    
                    double totalAmount = 0;
                    double totalPrincipal = monthlyPayment * months; // 총 납입금

                    if (compoundCheckBox.isSelected()) {
                        // 복리 계산
                        totalAmount = calculateCompoundInterest(monthlyPayment, annualRate, months);
                    } else {
                        // 단리 계산
                        totalAmount = calculateSimpleInterest(totalPrincipal, annualRate, months);
                    }
                    
                    double interestEarned = totalAmount - totalPrincipal; // 얻은 이자
                    DecimalFormat df = new DecimalFormat("#,###");
                    resultLabel.setText("결과: 총액 ₩" + df.format(totalAmount) + 
                                         ", 원금 ₩" + df.format(totalPrincipal) + 
                                         ", 이자 ₩" + df.format(interestEarned));
                } catch (NumberFormatException ex) {
                    resultLabel.setText("유효한 숫자를 입력하세요.");
                }
            }
        });
        
        // 창 보이기
        frame.setVisible(true);
    }
    
    // 단리 이자 계산
    private static double calculateSimpleInterest(double totalPrincipal, double annualRate, int months) {
        // 단리 이자 계산
        double simpleInterest = totalPrincipal * annualRate; 
        return totalPrincipal + simpleInterest; // 총액 반환
    }

    // 복리 이자 계산
    private static double calculateCompoundInterest(double monthlyPayment, double annualRate, int months) {
        double totalAmount = 0;
        double monthlyRate = annualRate / 12; // 월 이율

        for (int i = 0; i < months; i++) {
            totalAmount = (totalAmount + monthlyPayment) * (1 + monthlyRate);
        }
        return totalAmount; // 총액 반환
    }
}