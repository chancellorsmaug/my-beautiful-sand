
!!! in prep_nlgs

      case(i_MAGNETIC_MP_REPELL)
         this(ik)%i_law = i_MAGNETIC_MP_REPELL
         this(ik)%gapREF = this(ik)%internal(1)

         if (this(ik)%gapREF .le. 1.D-18) then
            write(cout,555) ik,this(ik)%gapREF
            call FATERR(IAM,cout)
         end if

      case(i_MAGNETIC_MP_ATTRACT)
         this(ik)%i_law = i_MAGNETIC_MP_ATTRACT
         this(ik)%gapREF = this(ik)%internal(1)

         if (this(ik)%gapREF .le. 1.D-18) then
            write(cout,555) ik,this(ik)%gapREF
            call FATERR(IAM,cout)
         end if


!!!  in solve_nlgs

   !!! --------------------------------------
         case(i_MAGNETIC_MP_REPELL)
            call get_Qm(ibehav, Qm)

            if (this(ik)%statusBEGIN .eq. i_noctc .or. &
                this(ik)%statusBEGIN .eq. i_nknow .or. &
                this(ik)%statusBEGIN .eq. i_vnish) then
               AA = (Qm**2)*H

               ! G 
               Tnn= 1 - (2*AA*this(ik)%Wnn*H / (this(ik)%gapREF**3))
               Tnt=0.d0
               Ttn= - (2*AA*this(ik)%Wtn*H / (this(ik)%gapREF**3))
               Ttt=1.d0

               ! G^-1
               detJ=Tnn*Ttt-Tnt*Ttn
               
               Ann=Ttt/detJ
               Ant=-Tnt/detJ
               Atn=-Ttn/detJ
               Att=Tnn/detJ

               ! ufree
               un=(vvlocfreenik - this(ik)%Wnn*AA/(this(ik)%gapREF**2))*Ann + (vvlocfreetik - this(ik)%Wtn*AA/(this(ik)%gapREF**2))*Ant
               ut=(vvlocfreenik - this(ik)%Wnn*AA/(this(ik)%gapREF**2))*Atn + (vvlocfreetik - this(ik)%Wtn*AA/(this(ik)%gapREF**2))*Att

               vvlocfreenik=un
               vvlocfreetik=ut

               ! W = G^-1 * W
               Tnn = Ann*WWnnik + Ant*WWtnik
               Ttt = (Att * WWttik) + (Atn * WWntik)
               Ttn = (Att * WWtnik) + (Atn * WWnnik)
               Tnt = (Ant * WWttik) + (Ann * WWntik)

               WWttik = Ttt; WWtnik = Ttn
               WWntik = Tnt; WWnnik = Tnn

               det = (WWttik*WWnnik)-(WWtnik*WWntik)
            
               forward  = WWnnik - (fricik*WWntik)
               if (forward .le. 1.D-18) forward = 0.d0
               backward = WWnnik + (fricik*WWntik)
               if (backward .le. 1.D-18) backward=0.d0


               
            
            else
               det      = this(ik)%det
               forward  = this(ik)%forward
               backward = this(ik)%backward
            
               ut = 0.d0
               un = 0.d0

            end if

            ! print*, AA, vvlocfreenik, un, this(ik)%gapREF            

            call mu_SC_std_solver_(det,forward,backward, &
                                   fricik, WWttik,WWtnik,WWntik,WWnnik,vvlocfreetik,vvlocfreenik, &
                                   sstatusik,rrltik,rrlnik,err)
            
            if (err /=0) then
              call LOGMES(' ') 
              write(cout,'(1x,"WWnn= ",D14.7," WWnt= ",D14.7)') WWnnik,WWntik
              call LOGMES(cout)
              write(cout,'(1x,"WWtn= ",D14.7," WWtt= ",D14.7)') WWtnik,WWttik
              call LOGMES(cout)
              call LOGMES(' ') 
              write(cout,'("fric= ",D14.7)') fricik
              call LOGMES(cout)
              call LOGMES(' ')               
              write(cout,'("vvlocfreen= ",D14.7," vvlocfreet= ",D14.7)') vvlocfreenik,vvlocfreetik
              call LOGMES(cout)
              call LOGMES(' ')               
              write(cout,'("gap= ",D14.7)') this(ik)%gapTTbegin
              call LOGMES(cout)
              call LOGMES(' ')
              call print_info_(ik)
            endif 

            if (err == 1) then
              call LOGMES(' ')
              write(cout,"(1X,'   WWnn(',I5,') - fric(',I5,')*Wnt(',I5,') < 1.D-18')") ik,ik,ik               
              call LOGMES(cout)
              write(cout,"('contact ',I0,' forward impossible')") ik
              call FATERR(IAM,cout)
            endif              
            if (err ==-1) then
              call LOGMES(' ')
              write(cout,"(1X,'   WWnn(',I5,') + fric(',I5,')*Wnt(',I5,') < 1.D-18')") ik,ik,ik
              call LOGMES(cout)
              write(cout,"('contact ',I0,' backward impossible')") ik               
              call FATERR(IAM,cout)
            endif
            if (err == 3) then
              call LOGMES(' ')
              call FATERR(IAM,'wtf')
            endif
           
         case(i_MAGNETIC_MP_ATTRACT)
            call get_Qm(ibehav, Qm)

            if (this(ik)%statusBEGIN .eq. i_noctc .or. &
            this(ik)%statusBEGIN .eq. i_nknow .or. &
            this(ik)%statusBEGIN .eq. i_vnish) then
               AA = -(Qm**2)*H

               ! G 
               Tnn= 1 - (2*AA*this(ik)%Wnn*H / (this(ik)%gapREF**3))
               Tnt=0.d0
               Ttn= - (2*AA*this(ik)%Wtn*H / (this(ik)%gapREF**3))
               Ttt=1.d0

               ! G^-1
               detJ=Tnn*Ttt-Tnt*Ttn
               
               Ann=Ttt/detJ
               Ant=-Tnt/detJ
               Atn=-Ttn/detJ
               Att=Tnn/detJ

               ! ufree 
               un=(vvlocfreenik - this(ik)%Wnn*AA/(this(ik)%gapREF**2))*Ann + (vvlocfreetik - this(ik)%Wtn*AA/(this(ik)%gapREF**2))*Ant
               ut=(vvlocfreenik - this(ik)%Wnn*AA/(this(ik)%gapREF**2))*Atn + (vvlocfreetik - this(ik)%Wtn*AA/(this(ik)%gapREF**2))*Att

               vvlocfreenik=un
               vvlocfreetik=ut

               ! W = G^-1 * W
               Tnn = Ann*WWnnik + Ant*WWtnik
               Ttt = (Att * WWttik) + (Atn * WWntik)
               Ttn = (Att * WWtnik) + (Atn * WWnnik)
               Tnt = (Ant * WWttik) + (Ann * WWntik)

               WWttik = Ttt; WWtnik = Ttn
               WWntik = Tnt; WWnnik = Tnn

               det = (WWttik*WWnnik)-(WWtnik*WWntik)
               
               forward  = WWnnik - (fricik*WWntik)
               if (forward .le. 1.D-18) forward = 0.d0
               backward = WWnnik + (fricik*WWntik)
               if (backward .le. 1.D-18) backward=0.d0

            else 
               det      = this(ik)%det
               forward  = this(ik)%forward
               backward = this(ik)%backward

               un = 0.d0
               ut = 0.d0

            end if

            ! print*, AA, vvlocfreenik, un, this(ik)%gapREF


            call mu_SC_std_solver_(det,forward,backward, &
                                   fricik, WWttik,WWtnik,WWntik,WWnnik,vvlocfreetik,vvlocfreenik, &
                                   sstatusik,rrltik,rrlnik,err)
            
            if (err /=0) then
              call LOGMES(' ') 
              write(cout,'(1x,"WWnn= ",D14.7," WWnt= ",D14.7)') WWnnik,WWntik
              call LOGMES(cout)
              write(cout,'(1x,"WWtn= ",D14.7," WWtt= ",D14.7)') WWtnik,WWttik
              call LOGMES(cout)
              call LOGMES(' ') 
              write(cout,'("fric= ",D14.7)') fricik
              call LOGMES(cout)
              call LOGMES(' ')               
              write(cout,'("vvlocfreen= ",D14.7," vvlocfreet= ",D14.7)') vvlocfreenik,vvlocfreetik
              call LOGMES(cout)
              call LOGMES(' ')               
              write(cout,'("gap= ",D14.7)') this(ik)%gapTTbegin
              call LOGMES(cout)
              call LOGMES(' ')
              call print_info_(ik)
            endif 

            if (err == 1) then
              call LOGMES(' ')
              write(cout,"(1X,'   WWnn(',I5,') - fric(',I5,')*Wnt(',I5,') < 1.D-18')") ik,ik,ik               
              call LOGMES(cout)
              write(cout,"('contact ',I0,' forward impossible')") ik
              call FATERR(IAM,cout)
            endif              
            if (err ==-1) then
              call LOGMES(' ')
              write(cout,"(1X,'   WWnn(',I5,') + fric(',I5,')*Wnt(',I5,') < 1.D-18')") ik,ik,ik
              call LOGMES(cout)
              write(cout,"('contact ',I0,' backward impossible')") ik               
              call FATERR(IAM,cout)
            endif
            if (err == 3) then
              call LOGMES(' ')
              call FATERR(IAM,'wtf')
            endif

!!! in solve_nlgs
   !!! ------------------------------------
         case(i_MAGNETIC_MP_REPELL) 
            ! if (Qm .lt. 0) then
               ! call FATERR(IAM, 'Qm < 0')
            ! else
            vn = vvlocfreenik + ((WWntik*rrltik) + (WWnnik*rrlnik)) ! normal velocity :D 
            if (this(ik)%statusBEGIN .eq. i_noctc .or. &
            this(ik)%statusBEGIN .eq. i_nknow .or. &
            this(ik)%statusBEGIN .eq. i_vnish) then
               this(ik)%corln = (Qm**2)*H*( 2*H*vn/(this(ik)%gapREF**3) - 1/this(ik)%gapREF**2)
            else 
               this(ik)%corln = 0.d0
            end if
            
            
            rlniki = rrlnik + this(ik)%corln
            rltiki = rrltik

         case(i_MAGNETIC_MP_ATTRACT) 
            ! if (Qm .lt. 0) then
            vn = vvlocfreenik + ((WWntik*rrltik) + (WWnnik*rrlnik))
            if (this(ik)%statusBEGIN .eq. i_noctc .or. &
            this(ik)%statusBEGIN .eq. i_nknow .or. &
            this(ik)%statusBEGIN .eq. i_vnish) then
               this(ik)%corln = - (Qm**2)*H*( 2*H*vn/(this(ik)%gapREF**3) - 1/this(ik)%gapREF**2)
            else 
               this(ik)%corln = 0.d0
            end if
            ! else
               ! call FATERR(IAM,'Qm > 0')
            ! end if
            
            rlniki = rrlnik + this(ik)%corln
            rltiki = rrltik

